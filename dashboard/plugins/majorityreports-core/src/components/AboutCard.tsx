import React from 'react';

import { InfoCard, Progress } from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { Namespace, Actor, Event, Feedback, Item } from '@internal/backstage-plugin-majorityreports-common';

import { AboutField } from './AboutField';
import { Tags } from './Tags';

function isNamespace(object: Namespace | Actor | Item | Event | Feedback): object is Namespace {
  return object.kind === "Namespace";
}

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
        <AboutField label="Title" value={object.meta?.title} gridSizes={{ xs: 12 }} />
        <AboutField label="Name" value={object.meta?.name} gridSizes={{ xs: 12, sm: 6 }} />
        <AboutField label="UID" value={object.meta?.uid} gridSizes={{ xs: 12, sm: 6 }} />

        <AboutField label="Tags" gridSizes={{ xs: 12, sm: 6 }}>
          <Tags object={object} />
        </AboutField>

        <AboutField label="Created" value={object.meta?.creationTimestamp?.toString()} gridSizes={{ xs: 12, sm: 6 }} />
        <AboutField label="Updated" value={object.meta?.updateTimestamp?.toString()} gridSizes={{ xs: 12, sm: 6 }} />
        {object.meta?.deletedTimestamp ? <AboutField label="Deleted" value={object.meta.deletedTimestamp?.toString()} gridSizes={{ xs: 12, sm: 6 }} /> : null}

        {isNamespace(object) ? (
          <>
            {object.spec?.lifecycle ? <AboutField label="Lifecycle" value={object.spec.lifecycle} gridSizes={{ xs: 12, sm: 6 }} /> : null}
            {object.spec?.owner ? <AboutField label="Owner" value={object.spec.owner} gridSizes={{ xs: 12 }} /> : null}
            {object.spec?.contact ? <AboutField label="Contact" value={object.spec.contact} gridSizes={{ xs: 12 }} /> : null}
          </>
        ) : null}
      </Grid>
    </InfoCard>
  );
}
