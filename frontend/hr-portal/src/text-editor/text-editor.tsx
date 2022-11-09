import * as React from 'react';
import {Editor} from 'draft-js';
import {useEditorApi} from './context';
import './text-editor.scss';
import cn from 'classnames';
import '../init';
export type TextEditorProps = {
  className?: string;
}

export const TextEditor: React.FC<TextEditorProps> = ({className}) => {
  const editorApi = useEditorApi();

  return (
    <div className={cn('text-editor', className)}>
      <Editor
        placeholder="Введите ваш текст"
        editorState={editorApi.state}
        onChange={editorApi.onChange}
        handleKeyCommand={editorApi.handleKeyCommand}
      />
    </div>
  );
};

export default TextEditor;