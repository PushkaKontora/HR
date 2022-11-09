import React from 'react';
import {TextEditorProvider} from '../../text-editor/context';
import ToolPanel from '../../tool-panel/tool-panel';
import TextEditor from '../../text-editor/text-editor';
import '../../init';

function EmployerCreatingNewVacancy() {
  return (
    <div>
      fff
      <TextEditorProvider>
        <ToolPanel/>
        <TextEditor/>
      </TextEditorProvider>
    </div>
  );
}

export default EmployerCreatingNewVacancy;