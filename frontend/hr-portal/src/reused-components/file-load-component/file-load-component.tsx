import {FileLoadInput} from '../../components/file-load-form/file-load-input';
import {ResumeTitle} from '../../components/styled/resume/resume-title';
import {RESUME_FORMATS} from '../../const/approved-file-formats';
import {useRef, useState} from 'react';
import {ComponentParent} from './styled/styles';
import {LoadButton} from '../load-button/load-button';
import {toast} from 'react-toastify';
import {useAppSelector} from '../../app/hooks';
import {DeleteButton} from '../delete-button/delete-button';

type FileLoadComponentProps = {
  fieldName: string,
  initFileName?: string,
  register: any,
  onUpdate: (file: File | null | undefined) => void,
  onDelete: () => Promise<void>
}

export function FileLoadComponent({fieldName, initFileName, register, onUpdate, onDelete}: FileLoadComponentProps) {
  const fileRef = useRef<HTMLInputElement | null>(null);
  const [fileName, setFileName] = useState<string | undefined>(initFileName);

  const update = (file: File | null | undefined) => {
    setFileName(file?.name);
    onUpdate(file);
  };

  const openFileDialog = () =>{
    if (fileRef?.current) {
      fileRef.current?.click();
    }
  };

  const deleteFile = () => {
    onDelete()
      .then(() => setFileName(''));
  };

  return (
    <ComponentParent>
      {fileName && <ResumeTitle>{fileName}</ResumeTitle>}
      <FileLoadInput register={register} formats={RESUME_FORMATS} onFileChange={update} inputRef={fileRef} name={fieldName}/>
      {fileName && <DeleteButton onClick={deleteFile}/>}
      <LoadButton onClick={openFileDialog}/>
    </ComponentParent>
  );
}