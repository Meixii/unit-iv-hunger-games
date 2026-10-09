#!/usr/bin/env bash
#
# sync-server.sh: Bidirectional Git sync & deployment for EvoSim Documentation
#
# Supports:
#   - Pushing CMS auto-commits from home server to GitHub (origin)
#   - Pulling/rebasing CMS content locally
#   - Pushing local commits (dev / main) to GitHub
#   - Updating home server safely with `git pull --rebase --autostash`
#   - Merging/fast-forwarding dev to main for production releases
#   - Managing and verifying Docker container health on port 8092
#
set -euo pipefail

# --- Configuration ---
SERVER_HOST="${EVOSIM_SERVER:-mika@100.118.20.19}"
SERVER_PATH="${EVOSIM_REMOTE_DIR:-~/Projects/unit-iv-hunger-games}"
CONTAINER_PORT="8092"
SSH_TIMEOUT="${SSH_TIMEOUT:-6}"

# --- ANSI Colors ---
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_GREEN="\033[32m"
C_BLUE="\033[34m"
C_YELLOW="\033[33m"
C_RED="\033[31m"
C_CYAN="\033[36m"

log_info()  { echo -e "${C_BLUE}ℹ${C_RESET}  $*"; }
log_ok()    { echo -e "${C_GREEN}✔${C_RESET}  $*"; }
log_warn()  { echo -e "${C_YELLOW}⚠${C_RESET}  $*"; }
log_err()   { echo -e "${C_RED}✖${C_RESET}  $*"; }
log_step()  { echo -e "\n${C_BOLD}${C_CYAN}==>${C_RESET} ${C_BOLD}$*${C_RESET}"; }

# --- Resolve Root ---
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$REPO_ROOT"

check_ssh() {
    if ! ssh -o ConnectTimeout="$SSH_TIMEOUT" -o BatchMode=yes "$SERVER_HOST" "bash -c 'exit 0'" 2>/dev/null; then
        log_err "Cannot reach home server at ${C_BOLD}${SERVER_HOST}${C_RESET} (timeout: ${SSH_TIMEOUT}s)."
        log_err "Verify Tailscale connectivity or server status."
        return 1
    fi
    return 0
}

run_remote() {
    local cmd="$1"
    ssh -o ConnectTimeout="$SSH_TIMEOUT" "$SERVER_HOST" "bash -c '${cmd}'"
}

cmd_status() {
    log_step "Checking Home Server & Container Status (${SERVER_HOST})"
    if ! check_ssh; then return 1; fi
    log_ok "SSH connection verified."

    log_info "Querying Docker container status..."
    run_remote "docker ps --filter 'name=evosim-docs' --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" || true

    log_info "Testing HTTP response on port ${CONTAINER_PORT}..."
    if run_remote "wget -qO- http://127.0.0.1:${CONTAINER_PORT}/admin >/dev/null 2>&1"; then
        log_ok "EvoSim Docs CMS responds healthy on port ${CONTAINER_PORT}!"
    else
        log_warn "Port ${CONTAINER_PORT} not yet responding (container may be initializing or stopped)."
    fi
}

cmd_pull() {
    log_step "Pulling Latest Commits from Origin"
    git pull --rebase origin dev || git pull --rebase origin main
    log_ok "Local branch updated."
}

cmd_push() {
    local do_merge=false
    local do_build=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -m|--merge) do_merge=true; shift ;;
            -b|--build) do_build=true; shift ;;
            *) shift ;;
        esac
    done

    log_step "Pushing Local Commits to GitHub"
    local current_branch
    current_branch="$(git rev-parse --abbrev-ref HEAD)"

    git push origin "$current_branch"
    git push --tags origin || true
    log_ok "Branch '${current_branch}' and tags pushed to origin."

    if [ "$do_merge" = true ] && [ "$current_branch" = "dev" ]; then
        log_step "Fast-Forwarding dev to main"
        git branch -f main dev
        git push origin main
        log_ok "Production branch 'main' updated."
    fi

    if [ "$do_build" = true ]; then
        cmd_deploy_server
    fi
}

cmd_deploy_server() {
    log_step "Deploying on Home Server via Tailscale (${SERVER_HOST})"
    if ! check_ssh; then return 1; fi

    log_info "Ensuring remote repository clone exists at ${SERVER_PATH}..."
    run_remote "
        if [ ! -d '${SERVER_PATH}' ]; then
            mkdir -p ~/Projects
            git clone git@github.com:Meixii/unit-iv-hunger-games.git '${SERVER_PATH}'
        fi
        cd '${SERVER_PATH}'
        git checkout main
        git pull --rebase origin main
    "

    log_info "Ensuring cms/.env exists on server..."
    run_remote "
        cd '${SERVER_PATH}/evosim-docs'
        if [ ! -f cms/.env ]; then
            cp cms/.env.example cms/.env
            sed -i 's/SERVE_DIST=false/SERVE_DIST=true/' cms/.env
        fi
    "

    log_info "Triggering Docker Compose build on server..."
    run_remote "
        cd '${SERVER_PATH}/evosim-docs'
        docker compose up -d --build
    "
    log_ok "Docker build command executed on server."

    sleep 3
    cmd_status
}

# --- CLI Dispatch ---
case "${1:-status}" in
    status) cmd_status ;;
    pull)   cmd_pull ;;
    push)   shift; cmd_push "$@" ;;
    deploy) shift; cmd_push -m -b "$@" ;;
    *)
        echo "Usage: $0 {status|pull|push [-m] [-b]|deploy}"
        exit 1
        ;;
esac
