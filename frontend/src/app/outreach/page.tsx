'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { apiClient, type Outreach, type Job } from '@/lib/api';
import { 
  Mail, 
  CheckCircle, 
  XCircle, 
  Clock, 
  Send,
  Eye,
  AlertCircle,
  Plus
} from 'lucide-react';

export default function OutreachPage() {
  const [outreachEmails, setOutreachEmails] = useState<Outreach[]>([]);
  const [jobs, setJobs] = useState<Record<number, Job>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedEmail, setSelectedEmail] = useState<Outreach | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [outreachData, jobsData] = await Promise.all([
          apiClient.getOutreachEmails(),
          apiClient.getJobs(0, 100)
        ]);
        
        setOutreachEmails(outreachData);
        
        // Create jobs lookup
        const jobsMap: Record<number, Job> = {};
        jobsData.forEach(job => {
          jobsMap[job.id] = job;
        });
        setJobs(jobsMap);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'approved':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'sent':
        return <Send className="h-4 w-4 text-blue-500" />;
      case 'rejected':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-yellow-500" />;
    }
  };

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'approved':
        return 'success';
      case 'sent':
        return 'default';
      case 'rejected':
        return 'destructive';
      default:
        return 'warning';
    }
  };

  const handleApprove = async (id: number) => {
    try {
      await apiClient.approveOutreachEmail(id);
      setOutreachEmails(prev => 
        prev.map(email => 
          email.id === id ? { ...email, status: 'approved' as const } : email
        )
      );
    } catch (err) {
      console.error('Failed to approve email:', err);
    }
  };

  const handleReject = async (id: number) => {
    try {
      await apiClient.rejectOutreachEmail(id);
      setOutreachEmails(prev => 
        prev.map(email => 
          email.id === id ? { ...email, status: 'rejected' as const } : email
        )
      );
    } catch (err) {
      console.error('Failed to reject email:', err);
    }
  };

  const handleGenerateAll = async () => {
    try {
      const response = await fetch('http://localhost:8000/outreach/generate-all', {
        method: 'POST',
      });
      const result = await response.json();
      alert(`Generated ${result.outreach_ids.length} outreach emails`);
      // Refresh the data
      window.location.reload();
    } catch (err) {
      console.error('Failed to generate emails:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-lg">Loading outreach emails...</p>
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
            <Button onClick={() => window.location.reload()} className="mt-4">
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
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Outreach Emails</h1>
              <p className="text-gray-600 mt-2">Manage and review outreach emails to potential clients</p>
            </div>
            <Button onClick={handleGenerateAll} className="flex items-center gap-2">
              <Plus className="h-4 w-4" />
              Generate All
            </Button>
          </div>
        </div>

        {/* Outreach Emails List */}
        <div className="space-y-6">
          {outreachEmails.map((email) => {
            const job = jobs[email.job_id];
            return (
              <Card key={email.id}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg">
                        {job ? `${job.title} at ${job.company}` : `Job ID: ${email.job_id}`}
                      </CardTitle>
                      <CardDescription className="flex items-center gap-4 mt-2">
                        <span className="flex items-center gap-1">
                          {getStatusIcon(email.status)}
                          <Badge variant={getStatusBadgeVariant(email.status)}>
                            {email.status}
                          </Badge>
                        </span>
                        {email.firm_contact && (
                          <span className="text-sm text-gray-600">
                            Contact: {email.firm_contact}
                          </span>
                        )}
                        <span className="text-sm text-gray-500">
                          Created: {new Date(email.created_at).toLocaleDateString()}
                        </span>
                      </CardDescription>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setSelectedEmail(email)}
                      >
                        <Eye className="h-4 w-4" />
                      </Button>
                      {email.status === 'draft' && (
                        <>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleApprove(email.id)}
                            className="text-green-600 hover:text-green-700"
                          >
                            <CheckCircle className="h-4 w-4" />
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleReject(email.id)}
                            className="text-red-600 hover:text-red-700"
                          >
                            <XCircle className="h-4 w-4" />
                          </Button>
                        </>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-gray-600 line-clamp-3">
                    {email.draft_email.split('\n').slice(2, 5).join('\n')}...
                  </div>
                </CardContent>
              </Card>
            );
          })}

          {outreachEmails.length === 0 && (
            <Card>
              <CardContent className="text-center py-12">
                <Mail className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No outreach emails found</h3>
                <p className="text-gray-600 mb-4">Generate outreach emails for high-confidence job matches.</p>
                <Button onClick={handleGenerateAll}>
                  Generate Outreach Emails
                </Button>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Email Preview Modal */}
        {selectedEmail && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <Card className="w-full max-w-4xl max-h-[80vh] overflow-y-auto">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Email Preview</CardTitle>
                  <Button variant="outline" onClick={() => setSelectedEmail(null)}>
                    Close
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <pre className="whitespace-pre-wrap text-sm font-mono">
                    {selectedEmail.draft_email}
                  </pre>
                </div>
                <div className="flex gap-2 mt-4">
                  {selectedEmail.status === 'draft' && (
                    <>
                      <Button onClick={() => handleApprove(selectedEmail.id)}>
                        Approve
                      </Button>
                      <Button variant="outline" onClick={() => handleReject(selectedEmail.id)}>
                        Reject
                      </Button>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
}
