import React from 'react';
import { useParams } from 'react-router-dom';

import {
  Page,
  Header,
  Content,
  ResponseErrorPanel,
} from '@backstage/core-components';

import Grid from '@material-ui/core/Grid';
// import Box from '@material-ui/core/Box';
// import Typography from '@material-ui/core/Typography';

import { useQuery } from '@tanstack/react-query';

import { Namespace } from '@internal/backstage-plugin-majorityreports-common';

import { AboutCard } from '../components/AboutCard';
import { DescriptionCard } from '../components/DescriptionCard';
import { LabelsCard } from '../components/LabelsCard';
import { AnnotationsCard } from '../components/AnnotationsCard';

// export const CountCard = () => {
//   return (
//     <InfoCard>
//       <Box textAlign="center">
//         <Typography variant="h6">23.123</Typography>
//         <Typography variant="h6">Actors</Typography>
//       </Box>
//     </InfoCard>
//   )
// }

export const NamespaceDetailsPage = () => {
  const { namespace_name: namespaceName } = useParams();

  const result = useQuery<Namespace>({
    queryKey: ['namespaces', namespaceName],
    queryFn: function getNamespaces() {
      const proxyUrl = 'http://localhost:7007/api/proxy/api/';
      const url = new URL('api/namespaces/' + namespaceName, proxyUrl);
      return fetch(url.toString()).then((response) => response.json());
    },
  });

  if (result.error) {
    return <ResponseErrorPanel error={result.error} />;
  }

  const namespace = result.data;

  return (
    <Page themeId="namespaces">
      <Header title={namespace?.meta?.title || namespace?.meta?.name} type="Namespace" typeLink="./.." />
      <Content>
        <Grid container>
          <Grid item container md={6}>
            <Grid item sm={12}>
              <AboutCard object={namespace} />
            </Grid>
            <Grid item sm={12}>
              <LabelsCard object={namespace} />
            </Grid>
            <Grid item sm={12}>
              <AnnotationsCard object={namespace} />
            </Grid>
          </Grid>
          <Grid item md={6}>
            {/* <Grid item md={6}>
              <CountCard />
            </Grid> */}
            <DescriptionCard object={namespace} />
          </Grid>
        </Grid>
      </Content>
    </Page>
  );
}
