import styled from 'styled-components';

export const Title = styled.h2<{marginTop: string}>`
  margin-top: ${props => props.marginTop};
  margin-bottom: 44px;
  margin-left: 0;
`;
