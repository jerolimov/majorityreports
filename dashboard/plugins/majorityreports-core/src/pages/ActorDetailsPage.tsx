import React from 'react';
import { useParams } from 'react-router-dom';
import useAsync from 'react-use/lib/useAsync';

import {
  Page,
  Header,
  Content,
  Progress,
  ResponseErrorPanel,
} from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { Actor } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';

export const ActorDetailsPage = () => {
  const { namespace_name: namespaceName, actor_name: actorName } = useParams();

  const { value: actor, loading, error } = useAsync(async (): Promise<Actor> => {
    const proxyUrl = 'http://localhost:7007/api/proxy/api/';
    const url = new URL('api/namespaces/' + namespaceName + '/actors/' + actorName, proxyUrl);
    return fetch(url.toString()).then((response) => response.json());
  }, []);

  if (loading) {
    return <Progress />;
  } else if (error) {
    return <ResponseErrorPanel error={error} />;
  }

  const title = actor?.annotations?.['title'] || actorName;

  return (
    <Page themeId="actor">
      <Header title={title} type="Actor" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item md={6}>
            <AboutCard object={actor} />
          </Grid>
          {/* <Grid item md={6}>
            <CountCard />
          </Grid> */}
          <Grid item md={6}>
            <DescriptionCard annotations={actor?.annotations} />
          </Grid>
          <Grid item md={6}>
            <LabelsCard labels={actor?.labels} />
          </Grid>
          <Grid item md={6}>
            <AnnotationsCard annotations={actor?.annotations} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
