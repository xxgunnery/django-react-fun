import type { NextPage } from "next"
import Head from "next/head"
import { Box, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react"
import React from "react"
import axios from "axios"
import SkillStats from "../components/SkillStats"

export default function Home() {

    return (
        <Tabs>
            <TabList>
                <Tab>
                    Skill Stats
                </Tab>
            </TabList>
            <TabPanels>
                <TabPanel>
                    <SkillStats />
                </TabPanel>
            </TabPanels>
        </Tabs>
    )
}

