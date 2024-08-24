import React from 'react';

import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

import { formatDate, formatRelative } from '../utils/date';

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
  value?: string | null;
  format?: "relativedatetime";
  gridSizes?: Record<string, number>;
  children?: React.ReactNode;
}

export function AboutField(props: AboutFieldProps) {
  const { label, value, format, gridSizes, children } = props;
  const classes = useStyles();

  // Content is either children or a string prop `value`
  let content: React.ReactNode;
  if (children) {
    content = children;
  } else if (format === 'relativedatetime' && value) {
    content = (
      <time dateTime={value} title={formatDate(value)}>
        {formatRelative(value)}
      </time>
    );
  } else if (value) {
    content = value;
  } else {
    content = "-";
  }

  return (
    <Grid item {...gridSizes}>
      <Typography variant="h2" className={classes.label}>
        {label}
      </Typography>
      <Typography variant="body2" className={classes.value}>
        {content}
      </Typography>
    </Grid>
  );
}
