import React from 'react';
import YAML from 'yaml'

import { InfoCard, Progress, CodeSnippet } from '@backstage/core-components';

import { Namespace, Actor, Event, Feedback, Item } from '@internal/backstage-plugin-majorityreports-common';

export const LabelsCard = ({ object }: { object?: Namespace | Actor | Item | Event | Feedback }) => {
  if (!object) {
    return (
      <InfoCard title="Labels">
        <Progress />
      </InfoCard>
    );
  }

  const labels = object.meta?.labels || {};

  return (
    <InfoCard title="Labels">
      <CodeSnippet text={YAML.stringify(labels)} language="yaml" showCopyCodeButton />
    </InfoCard>
  );
}
