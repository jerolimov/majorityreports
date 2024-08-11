import React from 'react';

import { InfoCard, Progress } from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { Namespace, Actor, Event, Feedback, Item } from '@internal/backstage-plugin-majorityreports-common';

import { AboutField } from './AboutField';
import { Tags } from './Tags';

export const AboutCard = ({ object }: { object?: Namespace | Actor | Item | Event | Feedback }) => {
  if (!object) {
    return (
      <InfoCard title="About">
        <Progress />
      </InfoCard>
    );
  }

  return (
    <InfoCard title="About">
      <Grid container>
        <AboutField label="Created" value={object.creationTimestamp?.toString()} gridSizes={{ xs: 12, sm: 6, lg: 4 }} />
        {/* <AboutField label="Updated" value={actor.updatedTimestamp?.toString()} gridSizes={{ xs: 12, sm: 6, lg: 4 }} /> */}
        {/* <AboutField label="Deleted" value={actor.deletionTimestamp?.toString()} gridSizes={{ xs: 12, sm: 6, lg: 4 }} /> */}
        <AboutField label="Tags" value={object.name} gridSizes={{ xs: 12, sm: 6, lg: 4 }}>
          <Tags object={object} />
        </AboutField>
      </Grid>
    </InfoCard>
  );
}
