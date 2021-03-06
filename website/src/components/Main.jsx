import React, { useState, useEffect } from "react"
import {
    BrowserRouter as Router,
    Routes,
    Route
  } from "react-router-dom"

import Navigation from './Navigation'
import Home from './Home'
import Settings from './Settings'
import Account from './Account'
import Posts from '../pages/Posts'
import Queues from '../pages/Queues'
import TAQueues from '../pages/TAQueues'
import StudentQueues from '../pages/StudentQueues'
import { FILL_PARENT, FILL_WIDTH } from "../utils/styles"
import { NAVBAR_HEIGHT } from "../utils/constants"

export default function Main({
    setAuthenticated,
    user
}) {
    
    const courses = ["CS 1110", "CS 2110", "CS 3110"]
    const [course, setCourse] = useState(0);
    const [userInfo, setUserInfo] = useState('');
    const [dimensions, setDimensions] = useState({ 
        height: window.innerHeight,
        width: window.innerWidth
    })

    const contentStyle = {
        ...FILL_PARENT
    }

    useEffect(() => {
        const handleResize = () => {
            setDimensions({
                height: window.innerHeight,
                width: window.innerWidth
            })
        }    
        window.addEventListener('resize', handleResize)
    })

    useEffect( () => {
        if (user.email) {
            fetch(`/users/one?email=${user.email}`)
            .then(resp => resp.json())
            .then(resp => {
                setUserInfo(resp)})
            .catch(err => console.log(err))
        }
    }, [user])

    return (
        <Router>
            <div>
                <div style={{...FILL_WIDTH, paddingTop: NAVBAR_HEIGHT, height: window.innerHeight - NAVBAR_HEIGHT}}>
                    <Routes>
                        <Route path="/students" element={<StudentQueues/>} />
                        <Route path="/instructor" element={<TAQueues/>} />
                        <Route path="/settings" element={<Settings />}/>
                        <Route path="/account" element={<Account />}/>
                        <Route path="/posts" element={<Posts />}/>
                        <Route path="/queues" element={<Queues user={user} />}/>
                        <Route path="/" element={<Posts />}/>
                    </Routes>
                </div>
                <Navigation 
                    setAuthenticated={setAuthenticated} 
                    courses={courses} 
                    setCourse={setCourse} 
                    courseIndex={course} 
                    userInfo={userInfo}/>
            </div>
        </Router>
    )
}