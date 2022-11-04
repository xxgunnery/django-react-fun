import { Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react"
import React from "react"
import PlayerDistribution from "../components/PlayerDistribution"
import SkillStats from "../components/SkillStats"

export default function Home() {

    return (
        <Tabs>
            <TabList>
                <Tab>
                    Skill Stats
                </Tab>
                <Tab>
                    Player Distribution
                </Tab>
            </TabList>
            <TabPanels>
                <TabPanel>
                    <SkillStats />
                </TabPanel>
                <TabPanel>
                    <PlayerDistribution />
                </TabPanel>
            </TabPanels>
        </Tabs>
    )
}

