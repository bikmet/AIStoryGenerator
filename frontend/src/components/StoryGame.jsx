import {useState, useEffect} from 'react';

//render story for us, and what happens when user wants new story
function StoryGame({story, onNewStory}) {
    const [currentNodeId, setCurrentNodeId] = useState(null)
    const [currentNode, setCurrentNode] = useState(null)
    const [options, setOptions] = useState([])
    const [isEnding, setIsEnding] = useState(false)
    const [isWinningEnding, setIsWinningEnding] = useState(false)

    useEffect( () => {
        if (story && story.root_node){
            const rootNodeId= story.root_node.id
            setCurrentNodeId(rootNodeId)


        }
    }, [story]) //everytime a story changes, root node changes

    useEffect( () => {
        if (currentNodeId && story && story.all_nodes){
            const node = story.all_nodes[currentNodeId]

            setCurrentNode(node)
            setIsEnding(node.is_ending)
            setIsWinningEnding(node.is_winning_ending)

            if(!node.is_ending && node.options && node.options.length > 0){
                setOptions(node.options)
            } else {
                setOptions([])
            }
        }
    }, [currentNodeId, story])

    const chooseOption = (optionID) => {
        setCurrentNodeId(optionID)
    }

    const restartStory = () => {
        if (story && story.root_node){
            setCurrentNodeId(story.root_node.id)
        }
    }

    return <div className="story-game">
        
                <header className="story-header">
                    <h2>{story.title}</h2>
                </header>

                {/*put the content of story here ending or options */}

                <div className="story-content">
                    {currentNode && /*there must be a current node to output story-node content*/
                    
                    <div className="story-node">
                        <p>{currentNode.content}</p>

                        {isEnding ? /*if an ending is achieved, display it that you've won or finished, else display options */
                        
                        <div className="story-ending">
                            <h3>{isWinningEnding ? "Congratulations" : "The End"}</h3>
                            {isWinningEnding ? "You reached a winning ending!" : "Your adventure has ended. "}

                        </div> : 

                            <div className="story-options">
                                <h3>What will you do?</h3>
                                <div className="options-list">
                                    {options.map((options, index) => {
                                        return <button 
                                                    key={index}
                                                    onClick={() => chooseOption(options.node_id)}
                                                    className="option-btn"
                                                    >
                                                    {options.text}
                                                </button>
                                    })}
                                </div>
                        </div>  }
                </div>}

                <div className ="story-controls">
                    <button onClick={restartStory} className = "reset-btn">
                        Restart Story
                    </button>
                </div>
                
                {onNewStory && 
                <button onClick={onNewStory} className="new-story-btn">
                    New Story
                </button>}
            </div>
        </div>}

        export default StoryGame