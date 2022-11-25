import {createSlice} from '@reduxjs/toolkit';

interface PageSlice {
  buttonVacancyCard: string;
}

const initialState: PageSlice = {
  buttonVacancyCard: ''
};

const pageSlice = createSlice({
  name: 'page',
  initialState,
  reducers: {
    setButtonVacancyCard(state, action) {
      state.buttonVacancyCard = action.payload;
    }
  }
});

export const {setButtonVacancyCard} = pageSlice.actions;

export default pageSlice.reducer;