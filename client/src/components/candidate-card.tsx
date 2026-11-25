"use client";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { Candidate } from "@/hooks/candidate";
import { cn } from "@/lib/utils";

type CandidateCardProps = {
  candidate: Candidate;
  isSelected: boolean;
  onSelect: (candidateId: string) => void;
};

// A card component that displays information about a candidate, including their initials, name,
// location, and statement. It also includes a button to select or deselect the candidate.
export function CandidateCard({
  candidate,
  isSelected,
  onSelect,
}: CandidateCardProps) {
  return (
    <Card
      className={cn(
        "transition-colors",
        isSelected && "border-primary ring-primary ring-1",
      )}
    >
      <CardHeader className="flex-row items-start gap-4 space-y-0">
        <div
          aria-hidden="true"
          className="bg-secondary text-secondary-foreground flex size-12 shrink-0 items-center justify-center rounded-full text-sm font-semibold"
        >
          {candidate.initials}
        </div>
        <div className="min-w-0">
          <CardTitle>{candidate.name}</CardTitle>
          <CardDescription className="mt-1">
            {candidate.location}
          </CardDescription>
        </div>
        <Button
          aria-pressed={isSelected}
          className="ml-auto shrink-0"
          onClick={() => onSelect(candidate.id)}
          size="sm"
          variant={isSelected ? "secondary" : "outline"}
        >
          {isSelected ? "Selected" : "Select"}
        </Button>
      </CardHeader>
      <CardContent>
        <p className="text-foreground/90 leading-7">{candidate.statement}</p>
      </CardContent>
    </Card>
  );
}
