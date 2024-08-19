import React from 'react';

import { InfoCard, MarkdownContent } from '@backstage/core-components';

import { Namespace, Actor, Event, Feedback, Item } from '@internal/backstage-plugin-majorityreports-common';

export const DescriptionCard = ({ object }: { object?: Namespace | Actor | Item | Event | Feedback }) => {
  const description = object?.meta?.description;

  if (!description) {
    return null;
  }

  return (
    <InfoCard title="Description">
      <MarkdownContent content={description} />
    </InfoCard>
  );
}
