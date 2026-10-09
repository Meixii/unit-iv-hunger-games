# One unified container: the CMS serves the built Astro documentation site.
# content/ and public/uploads are bind-mounted at runtime (see docker-compose.yml)
# so CMS edits persist across container restarts.
FROM node:22-alpine

WORKDIR /app

# git enables the CMS to auto-commit content saves (with .git bind-mounted)
RUN apk add --no-cache git

# Dependencies first for optimal Docker layer caching
COPY package.json package-lock.json ./
COPY cms/package.json cms/package.json
RUN npm ci

COPY . .
RUN npm run build

# Ensure non-root node user owns necessary writable runtime folders
RUN mkdir -p /app/public/uploads && chown -R node:node /app
USER node

EXPOSE 4000
CMD ["node", "cms/server.js"]
