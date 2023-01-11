import {CompetencyFlexContainer} from '../styled/values/competency-flex-container';
import {useEffect, useState} from 'react';
import {ClickableResumeTitle} from '../../reused-components/resume-title-clickable/resume-title-clickable';

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
            <ClickableResumeTitle key={idx} item={item} showDeleteButtons={showDeleteButtons} onDelete={() => {
              if (onDelete)
                onDelete(idx);
            }
            }/>);
        })
      }
    </CompetencyFlexContainer>
  );
}