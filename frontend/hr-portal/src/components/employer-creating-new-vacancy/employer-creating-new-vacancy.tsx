import '../../init';
import React, {useState} from 'react';
import {EditorState} from 'draft-js';
import {Editor} from 'react-draft-wysiwyg';
import DOMPurify from 'dompurify';

import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import {convertToHTML} from 'draft-convert';

function EmployerCreatingNewVacancy() {
  const [editorState, setEditorState] = useState(
    EditorState.createEmpty(),
  );
  const [convertedContent, setConvertedContent] = useState();

  const handleConvertContentToHTML = () => {
    const currentContentAsHTML = convertToHTML(editorState.getCurrentContent());
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    setConvertedContent(currentContentAsHTML);
  };

  const createMarkup = (html: any) => {
    return {
      __html: DOMPurify.sanitize(html)
    };
  };

  return (
    <div>
      редактируемое поле
      <Editor
        editorState={editorState}
        onEditorStateChange={setEditorState}
        toolbar={{
          options: ['inline', 'list'],
          inline: {
            inDropdown: false,
            className: 'inline-styles',
            component: undefined,
            dropdownClassName: undefined,
            options: ['bold', 'italic'],
            bold: {icon: 'B', className: 'bold-inline-fromServer'},
            italic: {icon: 'I', className: 'italic-inline-fromServer'},
          },
          list: {
            inDropdown: false,
            className: undefined,
            component: undefined,
            dropdownClassName: undefined,
            options: ['unordered', 'ordered'],
            unordered: {icon: 'U', className: 'unordered-list-fromServer'},
            ordered: {icon: 'O', className: 'ordered-unordered-fromServer'},
          }
        }}
      />
      <button onClick={handleConvertContentToHTML}>button</button>

      <div className="preview" dangerouslySetInnerHTML={createMarkup(convertedContent)}/>
    </div>
  );
}

export default EmployerCreatingNewVacancy;

//todo: настроить внешний вид по макетам