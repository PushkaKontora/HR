import {FileLoadInput} from '../components/file-load-form/file-load-input';
import {ResumeTitle} from '../components/styled/resume/resume-title';
import {RESUME_FORMATS} from '../const/approved-file-formats';
import {useRef, useState} from 'react';
import {ComponentParent} from './styled/styles';
import {LoadButton} from './load-button';

type FileLoadComponentProps = {
  fieldName: string,
  initFileName?: string,
  register: any,
  onUpdate: (file: File) => void
}

export function FileLoadComponent({fieldName, initFileName, register, onUpdate}: FileLoadComponentProps) {
  const fileRef = useRef<HTMLInputElement | null>(null);
  const [fileName, setFileName] = useState<string | undefined>(initFileName);

  const update = (file: File) => {
    setFileName(file.name);
    onUpdate(file);
  };

  const open = () =>{
    if (fileRef?.current) {
      fileRef.current?.click();
    }
  };

  return (
    <ComponentParent>
      {fileName && <ResumeTitle style={{marginRight: '8px'}}>{fileName}</ResumeTitle>}
      <FileLoadInput register={register} formats={RESUME_FORMATS} onFileChange={update} inputRef={fileRef} name={fieldName}/>
      <LoadButton onClick={open}/>
    </ComponentParent>
  );
}