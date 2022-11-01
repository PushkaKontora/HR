import styled from 'styled-components';

export const FormSubmit = styled.input`
  font-family: 'Graphik LCG', sans-serif;
  font-style: normal;
  font-weight: 600;
  font-size: 24px;
  line-height: 26px;

  background-color: #EF3420;
  width: 525px;
  height: 56px;
  
  text-align: center;
  border-radius: 10px;
  color: white;
  
  margin-bottom: 44px;
  
  &:hover {
    background-color: #F25847;
  }
  
  &:disabled {
    background-color: #F8A39A;
  }
  
  &:active {
    box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.2);
  }
`;