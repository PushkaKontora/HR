import { FormInputProps } from '../types/form-input-props';
import styled from 'styled-components';

const Parent = styled.div`
  margin-bottom: 32px;
`;

const InputField = styled.input`
  width: 525px;

  border: 1px solid #9C9C9C;
  border-radius: 0.8rem;
  background-color: white;

  padding: 20px;
  font-size: 18px;

  &:focus {
    border: 1px solid #4AC1FF;
  }

  &:invalid, &[aria-invalid='true'] {
    border: 1px solid #C52B1A;
  }
`;

const ErrorField = styled.div`
  font-size: 0.8rem;
  letter-spacing: 0.05em;
  
  margin-top: 0.5rem;
  margin-left: 0.5rem;
  
  color: #C52B1A;
  
  display: block;
`;

const LabelField = styled.label`
  font-size: 16px;
  letter-spacing: 0.05em;
  
  margin-bottom: 8px;
  
  display: block;
`;

function FormInput(props: FormInputProps) {
  const fieldName = props.name;

  return (
    <Parent>
      <LabelField>{props.label}</LabelField>
      <InputField type={props.type} {...props.register(props.name, props.options)} aria-invalid={props.errors[fieldName] ? 'true' : 'false'}/>
      <ErrorField>
        {[props.errors[fieldName]] && [props.errors[fieldName]?.message]}
      </ErrorField>
    </Parent>
  );
}

export default FormInput;
