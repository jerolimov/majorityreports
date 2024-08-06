import React from 'react';

import { Theme, useTheme } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Drawer from '@material-ui/core/Drawer';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import useMediaQuery from '@material-ui/core/useMediaQuery';
import FilterListIcon from '@material-ui/icons/FilterList';

export const FilterLayout = (props: { children: React.ReactNode }) => {
  return (
    <Grid container>
      {props.children}
    </Grid>
  );
}

FilterLayout.Filter = (props: { children: React.ReactNode }) => {
  const theme = useTheme();
  const isScreenSmallerThanBreakpoint = useMediaQuery((theme: Theme) =>
    theme.breakpoints.down('md'),
  );
  const [isDrawerOpen, setDrawerOpen] = React.useState<boolean>(false);

  if (isScreenSmallerThanBreakpoint) {
    return (
      <>
        <Button
          style={{ marginTop: theme.spacing(1), marginLeft: theme.spacing(1) }}
          onClick={() => setDrawerOpen(true)}
          startIcon={<FilterListIcon />}
        >
          Filters
        </Button>
        <Drawer
          open={isDrawerOpen}
          onClose={() => setDrawerOpen(false)}
          anchor="left"
          disableAutoFocus
          keepMounted
          variant="temporary"
        >
          <Box m={2}>
            <Typography
              variant="h6"
              component="h2"
              style={{ marginBottom: theme.spacing(1) }}
            >
              Filters
            </Typography>
            {props.children}
          </Box>
        </Drawer>
      </>
    );
  }

  return (
    <Grid item lg={2}>
      {props.children}
    </Grid>
  );
}

FilterLayout.Content = (props: { children: React.ReactNode }) => {
  return (
    <Grid item xs={12} lg={10}>
      {props.children}
    </Grid>
  );
}
