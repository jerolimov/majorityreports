import React from 'react';
import YAML from 'yaml'

import { InfoCard, Progress, CodeSnippet } from '@backstage/core-components';

import { Actor, Item } from '@internal/backstage-plugin-majorityreports-common';

export const FeaturesCard = ({ object }: { object?: Actor | Item }) => {
  if (!object) {
    return (
      <InfoCard title="Features">
        <Progress />
      </InfoCard>
    );
  }

  const features = object.spec?.features || {};

  return (
    <InfoCard title="Features">
      <CodeSnippet text={YAML.stringify(features)} language="yaml" showCopyCodeButton />
    </InfoCard>
  );
}
