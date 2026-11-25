"use client";

import Link from "next/link";
import { useState } from "react";

import { CandidateCard } from "@/components/candidate-card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useFetchCandidates } from "@/hooks/candidate";

// The main page component for displaying a list of candidates and allowing the user to select one.
export default function CandidatesPage() {
  const [selectedCandidateId, setSelectedCandidateId] = useState<string | null>(
    null,
  );

  const {
    data: candidates = [],
    isError,
    isFetching,
    isPending,
    refetch,
  } = useFetchCandidates();

  const selectedCandidate = candidates.find(
    (candidate) => candidate.id === selectedCandidateId,
  );

  return (
    <main className="bg-muted/30 relative min-h-screen px-4 py-10 sm:px-6 lg:px-8">
      <Button
        asChild
        className="absolute top-4 left-4 sm:top-6 sm:left-6"
        variant="ghost"
      >
        <Link href="/">← Back to home</Link>
      </Button>
      <section className="mx-auto max-w-3xl">
        <Badge className="mb-4" variant="secondary">
          Annual general meeting
        </Badge>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
          President candidates
        </h1>
        <p className="text-muted-foreground mt-3 max-w-2xl text-base sm:text-lg">
          Read each candidate’s statement before you cast your vote.
        </p>

        <div className="mt-6 flex justify-end">
          <Button
            disabled={isFetching}
            onClick={() => refetch()}
            type="button"
            variant="outline"
          >
            {isFetching ? "Refreshing candidates…" : "Refresh candidates"}
          </Button>
        </div>

        <div className="mt-4 space-y-4">
          {isPending &&
            Array.from({ length: 3 }, (_, index) => (
              <Card key={index}>
                <CardHeader className="flex-row items-start gap-4 space-y-0">
                  <div className="bg-muted size-12 animate-pulse rounded-full" />
                  <div className="min-w-0 flex-1 space-y-2 pt-1">
                    <div className="bg-muted h-5 w-40 animate-pulse rounded" />
                    <div className="bg-muted h-4 w-28 animate-pulse rounded" />
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="bg-muted h-4 animate-pulse rounded" />
                </CardContent>
              </Card>
            ))}

          {isError && (
            <Card className="border-destructive/40">
              <CardHeader>
                <CardTitle>Could not load candidates</CardTitle>
                <CardDescription>
                  Please try again before casting your vote.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Button onClick={() => refetch()} type="button">
                  Try again
                </Button>
              </CardContent>
            </Card>
          )}

          {!isPending &&
            !isError &&
            candidates.map((candidate) => (
              <CandidateCard
                candidate={candidate}
                isSelected={selectedCandidateId === candidate.id}
                key={candidate.id}
                onSelect={(candidateId) =>
                  setSelectedCandidateId((currentCandidateId) =>
                    currentCandidateId === candidateId ? null : candidateId,
                  )
                }
              />
            ))}
        </div>

        {selectedCandidate && (
          <div
            aria-live="polite"
            className="border-destructive/30 bg-destructive/5 mt-8 rounded-lg border p-5"
          >
            <p className="text-destructive text-sm font-medium">
              You have selected:
            </p>
            <p className="text-destructive mt-1 text-2xl font-bold">
              {selectedCandidate.name}
            </p>
          </div>
        )}

        <div className="mt-6 border-t pt-6">
          <Button
            className="w-full sm:w-auto"
            disabled={!selectedCandidate || isPending}
            size="lg"
            type="button"
          >
            Submit vote
          </Button>
        </div>
      </section>
    </main>
  );
}
