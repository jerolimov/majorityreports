import React from 'react';

import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(theme => ({
  value: {
    fontWeight: 'bold',
    overflow: 'hidden',
    lineHeight: '24px',
    wordBreak: 'break-word',
  },
  label: {
    color: theme.palette.text.secondary,
    textTransform: 'uppercase',
    fontSize: '10px',
    fontWeight: 'bold',
    letterSpacing: 0.5,
    overflow: 'hidden',
    whiteSpace: 'nowrap',
  },
}));

export interface AboutFieldProps {
  label: string;
  value?: string;
  gridSizes?: Record<string, number>;
  children?: React.ReactNode;
}

export function AboutField(props: AboutFieldProps) {
  const { label, value, gridSizes, children } = props;
  const classes = useStyles();

  // Content is either children or a string prop `value`
  const content = children ?? (
    <Typography variant="body2" className={classes.value}>
      {value || `unknown`}
    </Typography>
  );

  return (
    <Grid item {...gridSizes}>
      <Typography variant="h2" className={classes.label}>
        {label}
      </Typography>
      {content}
    </Grid>
  );
}
