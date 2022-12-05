import {ResumeTitle} from '../styled/resume/resume-title';
import {CompetencyFlexContainer} from '../styled/values/competency-flex-container';
import {ReactComponentElement, useEffect, useState} from 'react';
import deleteIcon from '../../assets/icons/delete-rounded.svg';
import {Icon} from './styles';
import {StyledComponent} from 'styled-components';

export type CompetencyListProps = {
  values: string[],
  showDeleteButtons: boolean,
  onDelete?: (index: number) => void
}

export function CompetencyList({values, showDeleteButtons, onDelete}: CompetencyListProps) {
  const [valuesState, setValuesState] = useState(values);

  useEffect(() => {
    setValuesState(values);
  }, [values]);

  return (
    <CompetencyFlexContainer>
      {
        valuesState.map((item, idx) => {
          return (
            <ResumeTitle style={{marginRight: '8px'}} key={idx}>
              <div>{item}</div>
              {showDeleteButtons && <button type={'button'} onClick={() => {
                if (onDelete) onDelete(idx);
              }}>
                <Icon src={deleteIcon}/>
              </button>}
            </ResumeTitle>);
        })
      }
    </CompetencyFlexContainer>
  );
}