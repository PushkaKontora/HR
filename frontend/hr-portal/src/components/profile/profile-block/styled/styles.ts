import styled from 'styled-components';
import {LargeRegular} from '../../../styled/fonts/large';

export const Parent = styled.section`
  width: 100%;
  
  margin-bottom: 80px;
  display: block;
`;

export const Title = styled.h4`
  margin-bottom: 16px;
`;

export const Description = styled(LargeRegular)`
  color: #9C9C9C;
`;

export const ButtonContainer = styled.article`
  display: flex;
  flex-wrap: nowrap;

  align-items: flex-start;
`;

export const Head = styled.section`
  width: 100%;
  
  display: flex;
  flex-wrap: nowrap;
  box-sizing: border-box;
`;