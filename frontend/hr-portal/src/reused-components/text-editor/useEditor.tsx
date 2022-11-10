import React, {useMemo} from 'react';
import DOMPurify from 'dompurify';

export type EditorApi = {
  fromHtml: () => any;
}

function UseEditor(html?: any): EditorApi {
  const fromHtml = () => {
    return {
      __html: DOMPurify.sanitize(html)
    };
  };

  return useMemo(
    () => ({
      fromHtml
    }),
    [
      fromHtml
    ]
  );
}

export default UseEditor;