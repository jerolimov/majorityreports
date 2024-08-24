import React from 'react';
import { setDefaultOptions, formatDate as _formatDate, formatRelative as _formatRelative } from "date-fns";
import { de } from 'date-fns/locale/de'

// TODO: make this configurable
setDefaultOptions({ locale: de });

export const formatDate = (date: Date | string | null | undefined) => {
  if (!date) {
    return "-";
  }
  return _formatDate(date, 'Pp');
}

export const formatRelative = (
  date: Date | string | null | undefined,
  baseDate?: Date,
) => {
  if (!date) {
    return "-";
  }
  if (!baseDate) {
    baseDate = new Date();
  }
  return _formatRelative(date, baseDate);
};

export const formatCreationTimestamp = (resource?: { meta?: { creationTimestamp?: string | null; } }) => {
  const value = resource?.meta?.creationTimestamp;
  if (!value) {
    return "-";
  }
  return (
    <time dateTime={value} title={formatDate(value)}>
      {formatRelative(value)}
    </time>
  )
};
