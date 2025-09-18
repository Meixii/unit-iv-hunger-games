import Link from "next/link";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";

interface NavigationItem {
  title: string;
  url: string;
}

interface PageNavigationProps {
  previous?: NavigationItem;
  next?: NavigationItem;
}

export function PageNavigation({ previous, next }: PageNavigationProps) {
  return (
    <div className="flex items-center justify-between border-t pt-6 mt-8">
      <div className="flex-1">
        {previous ? (
          <Link href={previous.url}>
            <Button variant="ghost" className="h-auto p-0 text-left justify-start">
              <ChevronLeft className="mr-2 h-4 w-4" />
              <div>
                <div className="text-sm text-muted-foreground">Previous</div>
                <div className="font-medium">{previous.title}</div>
              </div>
            </Button>
          </Link>
        ) : (
          <div />
        )}
      </div>
      
      <div className="flex-1 flex justify-end">
        {next ? (
          <Link href={next.url}>
            <Button variant="ghost" className="h-auto p-0 text-right justify-end">
              <div>
                <div className="text-sm text-muted-foreground">Next</div>
                <div className="font-medium">{next.title}</div>
              </div>
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        ) : (
          <div />
        )}
      </div>
    </div>
  );
}
