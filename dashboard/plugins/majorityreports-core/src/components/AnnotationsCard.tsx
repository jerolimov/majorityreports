import React from 'react';
import YAML from 'yaml'

import { InfoCard, Progress, CodeSnippet } from '@backstage/core-components';

import { Namespace, Actor, Event, Feedback, Item } from '@internal/backstage-plugin-majorityreports-common';

export const AnnotationsCard = ({ object }: { object?: Namespace | Actor | Item | Event | Feedback }) => {
  if (!object) {
    return (
      <InfoCard title="Annotations">
        <Progress />
      </InfoCard>
    );
  }

  const annotations = object.meta?.annotations || {};

  return (
    <InfoCard title="Annotations">
      <CodeSnippet text={YAML.stringify(annotations)} language="yaml" showCopyCodeButton />
    </InfoCard>
  );
}
