import { createContext, useState } from 'react';
import './App.css';

import Mobile from './mobile_invent/page';

export interface user {
        username: string,
        email: string,
        roles: Array<string>,
        store_role: Array<string>,
}

const baseUser: user = {
        username: 'test.user',
        email: 'email@example.ru',
        roles: ["MCC_RU_INSIGHT_IT_ROLE"],
        store_role: ["1014"],
}

export const UserContext = createContext<user>(baseUser);


function App() {

        return (
                <>
                        <UserContext.Provider value={baseUser}>
                                <Mobile />
                        </UserContext.Provider >
                </>
        )
}

export default App
