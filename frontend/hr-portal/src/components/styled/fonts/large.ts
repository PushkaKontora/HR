import styled from 'styled-components';

interface BtnWrapperProps {
  width?: string,
}

export const LargeRegular = styled.div.attrs<BtnWrapperProps>((props) => ({
  width: (props.width || '100%'),
}))<BtnWrapperProps>`
  font-weight: 400;
  font-size: 16px;
  line-height: 16px;
  letter-spacing: 0.05em;
  width: ${({width}) => width};
`;

export const LargeLight = styled(LargeRegular)`
  font-weight: 300;
`;

export const LargeMedium = styled(LargeRegular)`
  font-weight: 500;
`;
