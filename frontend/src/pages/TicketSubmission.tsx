import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { AlertCircle, CheckCircle, Send, Upload } from 'lucide-react';
import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { ClassificationPreview } from '../components/ClassificationPreview';
import { ticketAssistantAPI } from '../lib/api/client';
import { useClassification } from '../lib/hooks/useClassification';
import { ticketSubmissionSchema, type TicketSubmissionForm } from '../lib/schemas/ticketSchema';

const TicketSubmission: React.FC = () => {
  const [isSubmitted, setIsSubmitted] = useState(false);
  const queryClient = useQueryClient();

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
      return await ticketAssistantAPI.submitTicket({
        name: data.name,
        description: data.description,
        error_message: data.error_message,
        keywords,
        screenshot_url: data.screenshot_url
      });
    },
    onSuccess: () => {
      setIsSubmitted(true);
      queryClient.invalidateQueries({ queryKey: ['tickets'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
      reset();
    }
  });

  const onSubmit = (data: TicketSubmissionForm) => {
    submitMutation.mutate(data);
  };

  if (isSubmitted) {
    return (
      <div className="p-6">
        <div className="max-w-2xl mx-auto">
          <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
            <CheckCircle className="w-12 h-12 text-green-600 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-green-800 mb-2">Ticket Submitted Successfully!</h2>
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
                className="bg-gray-600 text-white px-6 py-2 rounded-lg hover:bg-gray-700 transition-colors"
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
    <div className="p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Submit a Support Ticket</h1>
          <p className="text-gray-600">
            Describe your issue and our AI will automatically classify and route it to the right team.
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Contact Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                  Your Name *
                </label>
                <input
                  {...register('name')}
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter your full name"
                />
                {errors.name && (
                  <p className="text-red-600 text-sm mt-1">{errors.name.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Email Address *
                </label>
                <input
                  {...register('email')}
                  type="email"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="your.email@example.com"
                />
                {errors.email && (
                  <p className="text-red-600 text-sm mt-1">{errors.email.message}</p>
                )}
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Issue Details</h2>
            <div className="space-y-4">
              <div>
                <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                  Issue Title *
                </label>
                <input
                  {...register('title')}
                  type="text"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Brief description of the issue"
                />
                {errors.title && (
                  <p className="text-red-600 text-sm mt-1">{errors.title.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                  Detailed Description *
                </label>
                <textarea
                  {...register('description')}
                  rows={5}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Please provide a detailed description of the issue, including steps to reproduce, expected behavior, and actual behavior..."
                />
                {errors.description && (
                  <p className="text-red-600 text-sm mt-1">{errors.description.message}</p>
                )}
              </div>

              <div>
                <label htmlFor="error_message" className="block text-sm font-medium text-gray-700 mb-1">
                  Error Message (Optional)
                </label>
                <textarea
                  {...register('error_message')}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Copy and paste any error messages you received..."
                />
              </div>

              <div>
                <label htmlFor="screenshot_url" className="block text-sm font-medium text-gray-700 mb-1">
                  Screenshot URL (Optional)
                </label>
                <div className="flex gap-2">
                  <input
                    {...register('screenshot_url')}
                    type="url"
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="https://example.com/screenshot.png"
                  />
                  <button
                    type="button"
                    className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors flex items-center gap-2"
                  >
                    <Upload className="w-4 h-4" />
                    Upload
                  </button>
                </div>
                {errors.screenshot_url && (
                  <p className="text-red-600 text-sm mt-1">{errors.screenshot_url.message}</p>
                )}
              </div>
            </div>
          </div>

          <ClassificationPreview
            classification={classification}
            isLoading={isClassifying}
            error={classificationError}
            isVisible={watchedDescription.length > 10}
          />

          <div className="bg-white p-6 rounded-lg shadow-sm border">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Ready to Submit?</h3>
                <p className="text-gray-600 text-sm">
                  Review your information and click submit to create your ticket.
                </p>
              </div>
              <button
                type="submit"
                disabled={!isValid || submitMutation.isPending}
                className={`px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors ${
                  isValid && !submitMutation.isPending
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                }`}
              >
                {submitMutation.isPending ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                    Submitting...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4" />
                    Submit Ticket
                  </>
                )}
              </button>
            </div>

            {submitMutation.isError && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-red-600" />
                <span className="text-red-700 text-sm">
                  Failed to submit ticket. Please try again.
                </span>
              </div>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

export default TicketSubmission;
