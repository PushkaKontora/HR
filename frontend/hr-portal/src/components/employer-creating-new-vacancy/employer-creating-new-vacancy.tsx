import '../../init';
import React, {useEffect, useState} from 'react';
import {ContentState, EditorState} from 'draft-js';
import {convertFromHTML, convertToHTML} from 'draft-convert';
import {Editor} from 'react-draft-wysiwyg';

import 'react-draft-wysiwyg/dist/react-draft-wysiwyg.css';
import './employer-creating-new-vacancy.scss';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setEditorTextVacancy} from '../../features/vacancy/vacancy-slice';
import {TypeRequestVacancyModal} from '../../const';

type EmployerCreatingNewVacancyProps = {
  typeViewToolbar: TypeRequestVacancyModal
}

function EmployerCreatingNewVacancy(props: EmployerCreatingNewVacancyProps) {
  const {typeViewToolbar} = props;
  const [editorState, setEditorState] = useState(
    EditorState.createEmpty()
  );
  const descriptionVacancy = useAppSelector((state) => state.vacancy.vacancyByID?.description);
  const isHiddenToolbar = useAppSelector((state) => state.vacancy.isHiddenToolbar);
  const isEditorVacancyFlag = useAppSelector((state) => state.vacancy.isEditorVacancyFlag);
  const typeOpenModal = useAppSelector((state) => state.vacancy.typeRequestModalVacancy);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (isEditorVacancyFlag) {
      const currentContentAsHTML = convertToHTML(editorState.getCurrentContent());
      dispatch(setEditorTextVacancy(currentContentAsHTML));
    }
  }, [isEditorVacancyFlag]);

  useEffect(() => {
    if (descriptionVacancy) {
      const blocksFromHTML = convertFromHTML(descriptionVacancy);
      const stateContent = ContentState.createFromBlockArray(
        blocksFromHTML.getBlocksAsArray(),
        blocksFromHTML.getEntityMap,
      );
      setEditorState(EditorState.createWithContent(stateContent));
    } else {
      setEditorState(EditorState.createEmpty());
    }
  }, [descriptionVacancy]);

  return (
    <div className="wrapper-employer-creating-new-vacancy">
      <div className="wrapper-editor-text">
        <Editor
          editorState={editorState}
          toolbarHidden={isHiddenToolbar || (typeViewToolbar !== typeOpenModal)}
          onEditorStateChange={setEditorState}
          placeholder="Описание вашей вакансии..."
          toolbar={{
            options: ['inline', 'list'],
            inline: {
              inDropdown: false,
              className: 'inline-styles',
              component: undefined,
              dropdownClassName: undefined,
              options: ['bold', 'italic'],
              bold: {className: 'icon-editor editor__bold', icon: null},
              italic: {className: 'icon-editor editor__italic', icon: null},
            },
            list: {
              inDropdown: false,
              className: undefined,
              component: undefined,
              dropdownClassName: undefined,
              options: ['unordered', 'ordered'],
              unordered: {className: 'icon-editor editor__unordered', icon: null},
              ordered: {className: 'icon-editor editor__ordered', icon: null}
            }
          }}
        />
      </div>
      {/*<button onClick={handleConvertContentToHTML}>button</button>*/}

      {/*<div className="preview" dangerouslySetInnerHTML={createMarkup(convertedContent)}/>*/}
    </div>
  );
}

export default EmployerCreatingNewVacancy;

//todo: настроить внешний вид по макетам