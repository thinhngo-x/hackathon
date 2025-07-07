import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { AlertCircle, CheckCircle, Send, Upload } from 'lucide-react';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { ClassificationPreview } from '../components/ClassificationPreview';
import { ticketAssistantAPI } from '../lib/api/client';
import { useToastContext } from '../lib/contexts/ToastContext';
import { useClassification } from '../lib/hooks/useClassification';
import { ticketSubmissionSchema, type TicketSubmissionForm } from '../lib/schemas/ticketSchema';

const TicketSubmission: React.FC = () => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const queryClient = useQueryClient();
  const { success, error } = useToastContext();

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isValid },
    reset
  } = useForm<TicketSubmissionForm>({
    resolver: zodResolver(ticketSubmissionSchema),
    mode: 'onChange'
  });

  const watchedDescription = watch('description', '');
  const watchedErrorMessage = watch('error_message', '');

  const { classification, isLoading: isClassifying, error: classificationError } = useClassification({
    description: watchedDescription,
    errorMessage: watchedErrorMessage
  });

  const submitMutation = useMutation({
    mutationFn: async (data: TicketSubmissionForm) => {
      const keywords = data.description.split(' ').filter(word => word.length > 3);

      // Use the new combined endpoint that classifies and creates ticket in database
      return await ticketAssistantAPI.submitTicketWithClassificationMock({
        name: data.name,
        description: data.description,
        error_message: data.error_message,
        keywords,
        screenshot_url: data.screenshot_url
      });
    },
    onSuccess: (response) => {
      setIsSubmitted(true);

      // Invalidate queries to refresh data
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
      success('Ticket Submitted Successfully!', response.ticket_id ? `Your ticket has been created with ID: ${response.ticket_id}` : 'Your ticket has been successfully submitted');
      reset();
    },
    onError: (err) => {
      error('Failed to Submit Ticket', err instanceof Error ? err.message : 'An unexpected error occurred');
    }
  });

  const onSubmit = (data: TicketSubmissionForm) => {
    submitMutation.mutate(data);
  };

  if (isSubmitted) {
    return (
      <div className="space-y-6">
        <div className="max-w-2xl mx-auto">
          <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-6 text-center">
            <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-green-600 mb-2">Ticket Submitted Successfully!</h2>
            <p className="text-green-600 mb-4">
              Your ticket has been submitted and automatically classified by our AI system.
            </p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => setIsSubmitted(false)}
                className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
              >
                Submit Another Ticket
              </button>
              <button
                onClick={() => window.location.href = '/tickets'}
                className="bg-muted text-muted-foreground px-6 py-2 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors"
              >
                View All Tickets
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-foreground mb-2">Submit a Support Ticket</h1>
          <p className="text-muted-foreground">
            Describe your issue and our AI will automatically classify and route it to the right team.
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Contact Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Your Name *</Label>
                  <Input
                    {...register('name')}
                    id="name"
                    placeholder="Enter your full name"
                  />
                  {errors.name && (
                    <p className="text-destructive text-sm">{errors.name.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email Address *</Label>
                  <Input
                    {...register('email')}
                    id="email"
                    type="email"
                    placeholder="your.email@example.com"
                  />
                  {errors.email && (
                    <p className="text-destructive text-sm">{errors.email.message}</p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Issue Details</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="title">Issue Title *</Label>
                <Input
                  {...register('title')}
                  id="title"
                  placeholder="Brief description of the issue"
                />
                {errors.title && (
                  <p className="text-destructive text-sm">{errors.title.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="description">Detailed Description *</Label>
                <Textarea
                  {...register('description')}
                  id="description"
                  rows={5}
                  placeholder="Please provide a detailed description of the issue, including steps to reproduce, expected behavior, and actual behavior..."
                />
                {errors.description && (
                  <p className="text-destructive text-sm">{errors.description.message}</p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="error_message">Error Message (Optional)</Label>
                <Textarea
                  {...register('error_message')}
                  id="error_message"
                  rows={3}
                  placeholder="Copy and paste any error messages you received..."
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="screenshot_url">Screenshot URL (Optional)</Label>
                <div className="flex gap-2">
                  <Input
                    {...register('screenshot_url')}
                    id="screenshot_url"
                    type="url"
                    className="flex-1"
                    placeholder="https://example.com/screenshot.png"
                  />
                  <Button type="button" variant="outline" size="sm">
                    <Upload className="w-4 h-4" />
                    Upload
                  </Button>
                </div>
                {errors.screenshot_url && (
                  <p className="text-destructive text-sm">{errors.screenshot_url.message}</p>
                )}
              </div>
            </CardContent>
          </Card>

          <ClassificationPreview
            classification={classification}
            isLoading={isClassifying}
            error={classificationError}
            isVisible={watchedDescription.length > 10}
          />

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold">Ready to Submit?</h3>
                  <p className="text-muted-foreground text-sm">
                    Review your information and click submit to create your ticket.
                  </p>
                </div>
                <Button
                  type="submit"
                  disabled={!isValid || submitMutation.isPending}
                  size="lg"
                >
                  {submitMutation.isPending ? (
                    <>
                      <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2" />
                      Submitting...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Submit Ticket
                    </>
                  )}
                </Button>
              </div>

              {submitMutation.isError && (
                <Alert variant="destructive" className="mt-4">
                  <AlertCircle className="w-4 h-4" />
                  <AlertDescription>
                    Failed to submit ticket. Please try again.
                  </AlertDescription>
                </Alert>
              )}
            </CardContent>
          </Card>
        </form>
      </div>
    </div>
  );
};

export default TicketSubmission;
