import type { ClassificationResponse } from '@shared/types/ticket';
import { AlertCircle, CheckCircle, Clock, Sparkles } from 'lucide-react';
import React from 'react';
import { departmentOptions, severityOptions } from '../lib/schemas/ticketSchema';

interface ClassificationPreviewProps {
  classification: ClassificationResponse | undefined;
  isLoading: boolean;
  error: Error | null;
  isVisible: boolean;
}

export const ClassificationPreview: React.FC<ClassificationPreviewProps> = ({
  classification,
  isLoading,
  error,
  isVisible
}) => {
  if (!isVisible) return null;

  const departmentLabel = departmentOptions.find(
    opt => opt.value === classification?.department
  )?.label;

  const severityOption = severityOptions.find(
    opt => opt.value === classification?.severity
  );

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-orange-600';
  };

  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4 mt-4">
      <div className="flex items-center gap-2 mb-3">
        <Sparkles className="w-5 h-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-gray-900">AI Classification</h3>
      </div>

      {isLoading && (
        <div className="flex items-center gap-2 text-blue-600">
          <Clock className="w-4 h-4 animate-spin" />
          <span>Analyzing your ticket...</span>
        </div>
      )}

      {error && (
        <div className="flex items-center gap-2 text-red-600">
          <AlertCircle className="w-4 h-4" />
          <span>Unable to classify at the moment</span>
        </div>
      )}

      {classification && (
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <span className="text-sm text-gray-600">Classification complete</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white p-3 rounded-lg shadow-sm">
              <div className="text-sm font-medium text-gray-500">Department</div>
              <div className="text-lg font-semibold text-gray-900">{departmentLabel}</div>
            </div>

            <div className="bg-white p-3 rounded-lg shadow-sm">
              <div className="text-sm font-medium text-gray-500">Severity</div>
              <div className={`text-lg font-semibold ${severityOption?.color}`}>
                {severityOption?.label}
              </div>
            </div>

            <div className="bg-white p-3 rounded-lg shadow-sm">
              <div className="text-sm font-medium text-gray-500">Confidence</div>
              <div className={`text-lg font-semibold ${getConfidenceColor(classification.confidence)}`}>
                {(classification.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          <div className="bg-white p-3 rounded-lg shadow-sm">
            <div className="text-sm font-medium text-gray-500 mb-1">AI Reasoning</div>
            <p className="text-sm text-gray-700">{classification.reasoning}</p>
          </div>

          {classification.suggested_actions && classification.suggested_actions.length > 0 && (
            <div className="bg-white p-3 rounded-lg shadow-sm">
              <div className="text-sm font-medium text-gray-500 mb-2">Suggested Actions</div>
              <ul className="space-y-1">
                {classification.suggested_actions.map((action, index) => (
                  <li key={index} className="text-sm text-gray-700 flex items-start gap-2">
                    <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                    {action}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
