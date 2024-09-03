import React from 'react';

import { InfoCard, Progress } from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { Namespace, src__items__types__Item as Item, Actor, Event, Feedback } from '@internal/backstage-plugin-majorityreports-common';

import { AboutField } from './AboutField';
import { Tags } from './Tags';

type AnyResource = Namespace | Item | Actor | Event | Feedback

function isNamespace(object: AnyResource): object is Namespace {
  return object.kind === "Namespace";
}

function isItem(object: AnyResource): object is Item {
  return object.kind === "Item";
}

function isActor(object: AnyResource): object is Actor {
  return object.kind === "Actor";
}

function isEvent(object: AnyResource): object is Event {
  return object.kind === "Event";
}

function isFeedback(object: AnyResource): object is Feedback {
  return object.kind === "Feedback";
}

export const AboutCard = ({ object }: { object?: AnyResource }) => {
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

        <AboutField label="Created" value={object.meta?.creationTimestamp} format="relativedatetime" gridSizes={{ xs: 12, sm: 6 }} />
        <AboutField label="Updated" value={object.meta?.updatedTimestamp} format="relativedatetime" gridSizes={{ xs: 12, sm: 6 }} />
        {object.meta?.deletedTimestamp ? <AboutField label="Deleted" value={object.meta.deletedTimestamp} format="relativedatetime" gridSizes={{ xs: 12, sm: 6 }} /> : null}

        {isNamespace(object) ? (
          <>
            {object.spec?.lifecycle ? <AboutField label="Lifecycle" value={object.spec.lifecycle} gridSizes={{ xs: 12, sm: 6 }} /> : null}
            {object.spec?.owner ? <AboutField label="Owner" value={object.spec.owner} gridSizes={{ xs: 12 }} /> : null}
            {object.spec?.contact ? <AboutField label="Contact" value={object.spec.contact} gridSizes={{ xs: 12 }} /> : null}
          </>
        ) : null}

        {isEvent(object) || isFeedback(object) ? (
          <>
            <AboutField label="Actor" value={object.spec.actor} gridSizes={{ xs: 12, sm: 6 }} />
            <AboutField label="Item" value={object.spec.item} gridSizes={{ xs: 12, sm: 6 }} />
          </>
        ) : null}

        {isItem(object) || isActor(object) || isEvent(object) || isFeedback(object) ? (
          <AboutField label="Type" value={object.spec.type} gridSizes={{ xs: 12, sm: 6 }} />
        ) : null}

        {isEvent(object) || isFeedback(object) ? (
          <AboutField label="Value" value={object.spec.value} gridSizes={{ xs: 12, sm: 6 }} />
        ) : null}
      </Grid>
    </InfoCard>
  );
}
