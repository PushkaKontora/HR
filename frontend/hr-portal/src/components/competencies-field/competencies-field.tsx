import Select, {OnChangeValue} from 'react-select';
import {useEffect, useState} from 'react';

import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setCompetencies} from '../../features/vacancy/vacancy-slice';
import './competencies-field.scss';
import CheckBoxImg from '../../assets/img/resume-page/Check_box.svg';
import {CompetenciesOption} from '../../features/resume/resume-slice';
import {getResumeList} from '../../service/async-actions/async-actions-resume';


function CompetenciesField() {
  const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
  const competenceList = useAppSelector((state) => state.resume.competenciesApi);
  const competencies = useAppSelector((state) => state.vacancy.paramsForGetVacancies.competencies);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(getResumeList());
  }, [competencies]);

  const handlerOnChangeValue = (newValues: OnChangeValue<CompetenciesOption, boolean>) => {
    const newCompetence = (newValues as CompetenciesOption[]).map((item: CompetenciesOption) => item.value);
    setSelectedOptions(newCompetence);
    dispatch(setCompetencies(newCompetence));
  };

  const handlerDeleteOnSelectedItem = (competence: string) => {
    const lineAriaLabel = `[aria-label="Remove ${competence}"]`;
    const elementCompetence = document.querySelector(lineAriaLabel);
    if (elementCompetence) {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      elementCompetence.click();
    }
  };

  return (
    <div className="filterItem filterItem__salary">
      <div className="filterItem-title">Компетенции</div>
      <div className="competencies-field-wrapper">
        <Select
          closeMenuOnSelect={true}
          // components={animatedComponents}
          // defaultValue={}
          hideSelectedOptions={true}
          isMulti
          options={competenceList}
          placeholder="Выбрать компетенцию"
          onChange={handlerOnChangeValue}
          classNamePrefix="custom-multiselect"
          tabSelectsValue={true}
        />
      </div>
      {
        selectedOptions.length > 0
          ? (
            <div className="selected-competence">
              {
                selectedOptions.map((competence, index) => (
                  <div key={index} className="selected-item-wrapper" onClick={() => handlerDeleteOnSelectedItem(competence)}>
                    <img src={CheckBoxImg} alt="check-box-item" className="checked-img"/>
                    <div className="name-competence">{competence}</div>
                  </div>
                ))
              }
            </div>
          ) : null
      }
    </div>
  );
}

export default CompetenciesField;