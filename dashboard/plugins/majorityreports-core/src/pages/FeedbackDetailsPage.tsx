import React from 'react';
import { useParams } from 'react-router-dom';

import {
  Page,
  Header,
  Content,
  Progress,
  ResponseErrorPanel,
} from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';

import { useQuery } from '@tanstack/react-query';

import { Feedback } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';

export const FeedbackDetailsPage = () => {
  const { namespace_name: namespaceName, feedback_name: feedbackName } = useParams();

  const result = useQuery<Feedback>({
    queryKey: ['feedbacks', namespaceName, feedbackName],
    queryFn: function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const url = new URL('api/namespaces/' + namespaceName + '/feedbacks/' + feedbackName, proxyUrl);
      return fetch(url.toString()).then((response) => response.json());
    },
  });

  if (result.isLoading) {
    return <Progress />;
  } else if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  const feedback = result.data;
  const title = feedback?.annotations?.['title'] || feedbackName;

  return (
    <Page themeId="feedback">
      <Header title={title} type="Feedback" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item md={6}>
            <AboutCard object={feedback} />
          </Grid>
          {/* <Grid item md={6}>
            <CountCard />
          </Grid> */}
          <Grid item md={6}>
            <DescriptionCard annotations={feedback?.annotations} />
          </Grid>
          <Grid item md={6}>
            <LabelsCard labels={feedback?.labels} />
          </Grid>
          <Grid item md={6}>
            <AnnotationsCard annotations={feedback?.annotations} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}