import React from 'react';

import {
  MarkdownContent,
  InfoCard,
} from '@backstage/core-components';

export const DescriptionCard = ({ annotations }: { annotations?: Record<string, string> }) => {
  const content = annotations?.['description'] ?? '# hello\n\n## hello 2';

  return (
    <InfoCard title="Description">
      <MarkdownContent content={content} />
    </InfoCard>
  );
}
