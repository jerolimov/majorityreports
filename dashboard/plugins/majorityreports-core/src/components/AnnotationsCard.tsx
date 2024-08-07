import React from 'react';
import YAML from 'yaml'

import {
  InfoCard,
  CodeSnippet,
} from '@backstage/core-components';

export const AnnotationsCard = ({ annotations }: { annotations?: Record<string, string> }) => {
  return (
    <InfoCard title="Annotations">
      <CodeSnippet text={YAML.stringify(annotations || { a: "sd" })} language="yaml" showCopyCodeButton />
    </InfoCard>
  );
}
