import Modal from '../../reused-components/modal/modal';
import React, {ChangeEvent, useEffect, useState} from 'react';
import {DepartmentsShortVersions, setSalaryMax, setSalaryMin, setStateEditVacancy} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import './modal-edit-vacancy.scss';
import cl from 'classnames';
import Select, {SingleValue} from 'react-select';
import {ExpectedExperience, ExpectedExperienceNameString} from '../../const';
import EmployerCreatingNewVacancy from '../employer-creating-new-vacancy/employer-creating-new-vacancy';

const expectedExperienceShortVersion = [
  {
    'value': 1,
    'label': ExpectedExperienceNameString[ExpectedExperience.NO_EXPERIENCE]
  },
  {
    'value': 2,
    'label': ExpectedExperienceNameString[ExpectedExperience.FROM_ONE_TO_THREE_YEARS]
  },
  {
    'value': 3,
    'label': ExpectedExperienceNameString[ExpectedExperience.FROM_THREE_TO_SIX_YEARS]
  },
  {
    'value': 4,
    'label': ExpectedExperienceNameString[ExpectedExperience.MORE_THAN_SIX_YEARS]
  },
];

function ModalEditVacancy() {
  const vacancyByID = useAppSelector((state) => state.vacancy.vacancyByID);
  const isPublishedVacancy = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const isOpenEditVacancyModalState = useAppSelector((state) => state.vacancy.isOpenEditVacancyModal);
  const [isOpenEditVacancyModal, setIsOpenEditVacancyModal] = useState(isOpenEditVacancyModalState);
  const dispatch = useAppDispatch();

  useEffect(() => {
    setIsOpenEditVacancyModal(isOpenEditVacancyModalState);
  }, [isOpenEditVacancyModalState]);

  useEffect(() => {
    dispatch(setStateEditVacancy(isOpenEditVacancyModal));
  }, [isOpenEditVacancyModal]);

  const onHandlerChangeExpectedExperience = (e: SingleValue<DepartmentsShortVersions>) => {
    //dispatch(setDepartmentParam(e?.label));
  };

  const handleChangeMinSalary = (e: ChangeEvent<HTMLInputElement>) => {
    //dispatch(setSalaryMin(e.target.value));
  };

  const handleChangeMaxSalary = (e: ChangeEvent<HTMLInputElement>) => {
    //dispatch(setSalaryMax(e.target.value));
  };

  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={1026}
      active={isOpenEditVacancyModal}
      setActive={setIsOpenEditVacancyModal}
    >
      <div className="edit-modal-item edit-modal-item__header">
        <div className="header header__title">Редактирование вакансии</div>
        <div className="header header__explanation">Заполните обязательные поля для создания вакансии</div>
      </div>
      <div className="edit-modal-item edit-modal-item__content">
        <div className="content-item">
          <div className="name-field">
            Статус вакансии*
          </div>
          <div className="toggleStatusVacancy">
            <button className={cl('btn-status', {'btn-status__active': isPublishedVacancy})}>
              Активна
            </button>
            <button className={cl('btn-status', {'btn-status__active': !isPublishedVacancy})}>
              Неактивна
            </button>
          </div>
        </div>
        <div className="content-item">
          <div className="name-field">
            Название вакансии*
          </div>
          <input
            type="text"
            placeholder={vacancyByID?.name}
            className="input-name-vacancy"
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Опыт работы*
          </div>
          <Select
            className="basic-single"
            classNamePrefix="select"
            name=""
            options={expectedExperienceShortVersion}
            onChange={onHandlerChangeExpectedExperience}
            placeholder={ExpectedExperienceNameString[vacancyByID?.expected_experience as ExpectedExperience]}
          />
        </div>
        <div className="content-item">
          <div className="name-field">
            Зарплата
          </div>
          <div className="salaryInput-wrapper">
            <div className="text-field-salary text-field-salary__min">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                value={vacancyByID?.salary_from !== 0 ? vacancyByID?.salary_from : 0}
                onChange={handleChangeMinSalary}
                placeholder="min"
              />
            </div>
            <div className="text-field-salary text-field-salary__max">
              <input
                className="text-field-salary-input"
                type="number"
                min="0"
                value={vacancyByID?.salary_to !== 0 ? vacancyByID?.salary_to : 0}
                onChange={handleChangeMaxSalary}
                placeholder="max"
              />
            </div>
          </div>
        </div>
        <div className="content-item content-item__description">
          <div className="name-field">
            Описание вакансии*
          </div>
          <EmployerCreatingNewVacancy/>
        </div>
      </div>
      <div className="edit-modal-item">

      </div>
    </Modal>
  );
}

export default ModalEditVacancy;