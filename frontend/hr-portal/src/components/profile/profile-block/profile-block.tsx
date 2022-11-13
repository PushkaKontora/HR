import {MutableRefObject, PropsWithChildren, RefObject} from 'react';
import {Head, Title, Description, ButtonContainer, Parent} from './styled/styles';
import {BlackButton} from '../../styled/buttons/black-button';

type ButtonData = {
  text: string,
  onClick: () => void,
  ref?: RefObject<any>,
  showing?: boolean
};

export type ProfileBlockProps = {
  title: string,
  description: string,
  buttons?: ButtonData[]
} & PropsWithChildren;

export function ProfileBlock(props: ProfileBlockProps) {
  return (
    <Parent>
      <Head>
        <div style={{flex: 1}}>
          <Title>{props.title}</Title>
          <Description>{props.description}</Description>
        </div>
        <ButtonContainer>
          {props.buttons && props.buttons.map((item, idx) =>
            <BlackButton key={idx} onClick={item.onClick} ref={item?.ref}>
              {item.text}
            </BlackButton>)}
        </ButtonContainer>
      </Head>
      <div style={{width: '100%', marginTop: '32px'}}>
        {props.children}
      </div>
    </Parent>
  );
}
