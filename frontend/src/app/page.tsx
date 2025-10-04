'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { apiClient, type Stats, type Job, type AgentMatch } from '@/lib/api';
import { 
  Building2, 
  Users, 
  Mail, 
  TrendingUp, 
  AlertCircle
} from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [recentJobs, setRecentJobs] = useState<Job[]>([]);
  const [recentMatches, setRecentMatches] = useState<AgentMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [statsData, jobsData, matchesData] = await Promise.all([
          apiClient.getStats(),
          apiClient.getJobs(0, 5),
          apiClient.getAgentMatches(undefined, undefined, 0, 5)
        ]);
        
        setStats(statsData);
        setRecentJobs(jobsData);
        setRecentMatches(matchesData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);


  const getAgentBadgeVariant = (agent: string) => {
    switch (agent) {
      case 'AFC':
        return 'default';
      case 'FSP':
        return 'secondary';
      default:
        return 'outline';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-lg">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Card className="w-96">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertCircle className="h-5 w-5 text-red-500" />
              Error
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-red-600">{error}</p>
            <Button 
              onClick={() => window.location.reload()} 
              className="mt-4"
            >
              Retry
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Auditor Job Posting Agent</h1>
          <p className="text-gray-600 mt-2">AI-powered job analysis and outreach system</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Jobs</CardTitle>
              <Building2 className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.jobs.total || 0}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Agent Matches</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.agent_matches.total || 0}</div>
              <div className="text-xs text-muted-foreground">
                AFC: {stats?.agent_matches.afc || 0} | FSP: {stats?.agent_matches.fsp || 0}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Outreach Emails</CardTitle>
              <Mail className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.outreach.total || 0}</div>
              <div className="text-xs text-muted-foreground">
                Draft: {stats?.outreach.draft || 0} | Approved: {stats?.outreach.approved || 0}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stats?.outreach.total ? 
                  Math.round(((stats.outreach.approved + stats.outreach.sent) / stats.outreach.total) * 100) : 0}%
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Jobs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Recent Job Postings</CardTitle>
              <CardDescription>Latest jobs processed by the system</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentJobs.map((job) => (
                  <div key={job.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium">{job.title}</h4>
                      <p className="text-sm text-gray-600">{job.company} • {job.location}</p>
                      <p className="text-sm text-green-600 font-medium">
                        ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
                      </p>
                    </div>
                    <Badge variant="outline">{job.source}</Badge>
                  </div>
                ))}
                {recentJobs.length === 0 && (
                  <p className="text-gray-500 text-center py-4">No jobs found</p>
                )}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Recent Agent Matches</CardTitle>
              <CardDescription>Latest AI-powered job-to-agent matches</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentMatches.map((match) => (
                  <div key={match.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant={getAgentBadgeVariant(match.matched_agent)}>
                          {match.matched_agent}
                        </Badge>
                        <span className="text-sm text-gray-600">
                          {Math.round(match.confidence_score * 100)}% confidence
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">Job ID: {match.job_id}</p>
                    </div>
                  </div>
                ))}
                {recentMatches.length === 0 && (
                  <p className="text-gray-500 text-center py-4">No matches found</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card className="mt-6">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>Common tasks and system operations</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-4">
              <Button>View All Jobs</Button>
              <Button variant="outline">View Agent Matches</Button>
              <Button variant="outline">Review Outreach</Button>
              <Button variant="outline">Generate New Jobs</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}