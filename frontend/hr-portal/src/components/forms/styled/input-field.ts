import styled from 'styled-components';

export type InputFieldProps = {
  normalBorderColor: string,
  padding: string
}

export const InputField = styled.input<InputFieldProps>`
  width: 525px;

  border: 1px solid ${props => props.normalBorderColor};
  border-radius: 0.8rem;
  background-color: white;

  padding: ${props => props.padding};

  &:focus {
    border: 1px solid #4AC1FF;
  }

  &:invalid, &[aria-invalid='true'] {
    border: 1px solid #C52B1A;
  }
  
  &::placeholder {
    color: #9C9C9C;
  }
`;
