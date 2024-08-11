import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const supportsNamespaces = ['actors', 'items', 'events', 'feedbacks'];

export function useNamespace(): [string | null, (newNamespace: string | null) => void] {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const namespace = pathname.startsWith('/namespaces/') ?
    pathname.split('/')[2] :
    null;

  const setNamespace = React.useCallback((newNamespace: string | null) => {
    let newPath: string | null = null;

    if (pathname.startsWith('/namespaces/')) {
      if (newNamespace) {
        newPath = '/namespaces/' + newNamespace + '/' + pathname.split('/').slice(3).join('/');
      } else {
        newPath = '/' + pathname.split('/').slice(3).join('/');
      }
    } else if (supportsNamespaces.includes(pathname.split('/')[1])) {
      if (newNamespace) {
        newPath = '/namespaces/' + newNamespace + pathname;
      }
    } else {
      if (newNamespace) {
        newPath = '/namespaces/' + newNamespace;
      }
    }

    if (newPath) {
      navigate(newPath)
    }
}, [pathname]);

  return [namespace, setNamespace];
}
