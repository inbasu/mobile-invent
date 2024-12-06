import { useState } from 'react';
import './App.css';

import Mobile from './mobile_invent/page';

function App() {
        const [count, setCount] = useState(0)

        return (
                <>
                        <Mobile />
                </>
        )
}

export default App
