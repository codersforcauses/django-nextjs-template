import { useQuery } from "@tanstack/react-query";

// A mock candidate data type from the server response.
export type Candidate = {
  id: string;
  initials: string;
  name: string;
  location: string;
  statement: string;
};

// Parameters for fetching candidates, including pagination options.
type CandidatesParams = {
  page?: number;
  pageSize?: number;
};

// Mock data for the president candidates.
const mockPresidentCandidates: Candidate[] = [
  {
    id: "alex-morgan",
    initials: "AM",
    name: "Alex Morgan",
    location: "Sydney, NSW",
    statement:
      "I want to make electric transport practical, accessible, and visible in communities across New South Wales.",
  },
  {
    id: "jordan-lee",
    initials: "JL",
    name: "Jordan Lee",
    location: "Newcastle, NSW",
    statement:
      "My focus is connecting members, strengthening local chapters, and supporting reliable charging infrastructure.",
  },
  {
    id: "samira-khan",
    initials: "SK",
    name: "Samira Khan",
    location: "Wollongong, NSW",
    statement:
      "I will bring a member-first approach to advocacy, education, and the transition to electric mobility.",
  },
];

// Simulates fetching candidates from an API endpoint with optional parameters.
async function fetchCandidates(
  params: CandidatesParams = {},
): Promise<Candidate[]> {
  // In a real application, you would replace this with an actual API call, for example:
  // const response = await api.get<Candidate[]>("/candidates/", { params: { page } });

  await new Promise((resolve) => setTimeout(resolve, 650));

  return mockPresidentCandidates;
}

// Custom hook to fetch candidates using React Query, with caching and retry logic.
function useFetchCandidates(params: CandidatesParams = {}) {
  return useQuery({
    queryKey: ["candidates", "president", params],
    queryFn: () => fetchCandidates(params),
    retry: false,
    staleTime: 30_000,
  });
}

export { useFetchCandidates };
