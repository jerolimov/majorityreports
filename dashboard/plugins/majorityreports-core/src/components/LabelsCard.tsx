import React from 'react';
import YAML from 'yaml'

import {
  InfoCard,
  CodeSnippet,
} from '@backstage/core-components';

export const LabelsCard = ({ labels }: { labels?: Record<string, string> }) => {
  return (
    <InfoCard title="Labels">
      <CodeSnippet text={YAML.stringify(labels || {})} language="yaml" showCopyCodeButton />
    </InfoCard>
  );
}
