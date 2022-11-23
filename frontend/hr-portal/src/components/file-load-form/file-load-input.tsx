import {useForm} from 'react-hook-form';
import {ChangeEvent, MutableRefObject} from 'react';

type FileLoadFormProps = {
  formats: string[],
  onFileChange: (file: File) => void,
  inputRef: MutableRefObject<HTMLInputElement | null>,
  name: string,
  register: any
}

export function FileLoadInput({formats, onFileChange, inputRef, name, register}: FileLoadFormProps) {
  const {ref, ...rest} = register(name);

  const onChange = (event: ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files && files.length == 1) {
      onFileChange(files[0]);
    }
  };

  return (
    <input
      {...rest}
      type="file"
      accept={formats.join(', ')}
      style={{display: 'none'}}
      ref={(e) => {
        ref(e);
        inputRef.current = e;
      }}
      onChange={onChange}/>
  );
}