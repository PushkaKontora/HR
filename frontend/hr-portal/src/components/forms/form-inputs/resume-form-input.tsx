import { FormInputProps } from '../types/form-input-props';
import styled from 'styled-components';
import {InputField} from '../styled/input-field';

const Parent = styled.div`
  display: inline-block;
  
  margin-bottom: 32px;
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

function AuthFormInput(props: FormInputProps) {
  const fieldName = props.name;

  return (
    <Parent>
      <LabelField>{props.label}</LabelField>
      <div>
        <InputField
          normalBorderColor={'black'}
          padding={'16px'}
          type={props.type}
          {...props.register(props.name, props.options)}
          aria-invalid={props.errors[fieldName] ? 'true' : 'false'}/>
        <ErrorField>
          {[props.errors[fieldName]] && [props.errors[fieldName]?.message]}
        </ErrorField>
      </div>
    </Parent>
  );
}

export default AuthFormInput;
